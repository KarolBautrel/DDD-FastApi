from fastapi import FastAPI
from db.db_metadata import start_mapper
import routes.shipping.shipping_routes as shipping

app = FastAPI()
start_mapper()


app.include_router(shipping.router)
