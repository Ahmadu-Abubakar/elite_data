from catalog.models import Catalog
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from .exceptions import *
import logging
from django.db import transaction


logger = logging.getLogger(__name__)


@dataclass
class Tracker:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    started_at: datetime = field(default_factory=datetime.now)
    finished_at: Optional[datetime] = None
    status: str = "RUNNING"

    def complete(self):
        self.status = "FINISHED"
        self.finished_at = datetime.now()

    def fail(self):
        self.status = "FAILED"
        self.finished_at = datetime.now()


class SynchronizationRun:
    def __init__(self):
        self.tracker = Tracker() 


    def _create(self, payload):
        instances = [
            Catalog(
                provider_plan_id=data["provider_plan_id"],
                provider=data["provider_name"],
                amount=data["amount"],
                price=data["price"],
                validity=data["validity"],
                duration_category=data["duration_category"],
                plan_type_category=data["plan_type_category"],
                availability=Catalog.ProductState.AVAILABLE,
                margin=data["margin"],
                supplier_price=data["supplier_price"],
            )
            for data in payload
            if data.get("amount") is not None
        ]

        Catalog.objects.bulk_create(instances)

        


    def _update(self, payload):
        instances = []

        for existing, incoming in payload:
            existing.provider = incoming["provider_name"]
            existing.amount = incoming["amount"]
            existing.price = incoming["price"]
            existing.validity = incoming["validity"]
            existing.duration_category = incoming["duration_category"]
            existing.plan_type_category = incoming["plan_type_category"]
            existing.margin = incoming["margin"]
            existing.supplier_price = incoming["supplier_price"]
           
            instances.append(existing)

        Catalog.objects.bulk_update(
            instances,
            [
                "provider",
                "amount",
                "price",
                "validity",
                "duration_category",
                "plan_type_category",
                "margin",
                "supplier_price",
            ]
        )


        


    def _mark_unavailable(self, failed_track):
        pass

        # if not failed_track:
        #     return

        # failed_track_id = [plan.id for plan in failed_track]

        # Catalog.objects.filter(id__in=failed_track_id).update(
        #     availability = Catalog.ProductState.UNAVAILABLE
        # )


    def _mark_available(self, products):
        if not products:
            return

        products_id = [plan.id for plan in products]

        Catalog.objects.filter(id__in=products_id).update(
            availability = Catalog.ProductState.AVAILABLE
        )



    def _compare(self, incoming_data):
        # the four containers 
        new_plan = []

        missing = []

        changed = []

        unchanged = []

        seen_plans = []


        # the actual data
        db_data = Catalog.objects.all()


        # lookups of those data
        db_lookup = {
            (plan.provider_plan_id, plan.provider) : plan 
            for plan in db_data 
        }

        incoming_lookup = {
            (plan["provider_plan_id"], plan["provider_name"]) : plan
            for plan in incoming_data
        }




        for key, db_plan in db_lookup.items():

            if key not in incoming_lookup.keys():

                missing.append(db_plan)
            else:
                seen_plans.append(db_plan)
        

        for key, incoming_plan in incoming_lookup.items():

            if key not in db_lookup: 

                new_plan.append(incoming_plan)

            else:

                db_plan = db_lookup[key]

                

                if (
                    db_plan.price != incoming_plan["price"]
                    or db_plan.margin != incoming_plan["margin"] 
                    or db_plan.validity != incoming_plan["validity"]
                    or db_plan.duration_category != incoming_plan["duration_category"]
                    or db_plan.plan_type_category != incoming_plan["plan_type_category"]
                    or db_plan.supplier_price  != incoming_plan["supplier_price"]
                    or db_plan.amount != incoming_plan["amount"]

                ) :

                    changed.append((db_plan, incoming_plan))

                else:
                    unchanged.append(incoming_plan)

        comparison_result  = {
            "new_plan" : new_plan,
            "unchanged"  : unchanged,
            "missing"  : missing,
            "changed"  : changed,
            "seen_plans" : seen_plans
        }
        return comparison_result

        

    
    def apply_changes(self, data):
        # the comparison result
        compared_data = self._compare(data)

        with transaction.atomic():
            self._create(compared_data["new_plan"])
            self._update(compared_data["changed"])
            self._mark_available(compared_data["seen_plans"])
            self._mark_unavailable(compared_data["missing"])


            # set tracker to success
            self.tracker.complete()

        
    
#  discoveries = discover_available_products()


    


