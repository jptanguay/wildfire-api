from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Union

import numpy as np
import pandas as pd

app = FastAPI(
    title="Wildfire",
    description="Feux de forêts - Canada - 1990 à 2021",
    summary="Simple queries on the full dataset",
    version="0.0.1",
    terms_of_service="",
    contact={
        "name": "jptanguay",
        "url": "https://github.com/jptanguay/wildfire-canada",
        "email": "test@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

def load_data():
    df = pd.read_csv("./wildfire-canada-1990-2021.csv")
    return df


#####################################


@app.get("/",    
    summary="root path",
    response_description="returns all the data from the dataset",
)
def read_root():
    df = load_data()    
    #return df.to_dict("records")
    data = df.query("year >= 1900")
    return data.to_dict("records")
    



@app.get("/jurisdictions/",    
    summary="list of jurisdictions",
    response_description="Array containing the jurisdictions",
)
def get_jurisdictions() -> list[str]:
    df = load_data()
    jur = df["jurisdiction"].unique() #.to_dict()
    return  jur ;




@app.get("/jurisdictions/{name}",    
    summary="Data for the jurisdiction in 'name'",
    response_description="Nothing",
)
def get_jurisdiction_data(name :str):

    df = load_data()
    
    valid_names = df["jurisdiction"].unique()
    if name not in valid_names:
        valid_names = ", ".join(get_jurisdictions())
        raise HTTPException(status_code=418, detail="Wrong name. Must be one of: " + valid_names)
        
    df = load_data()
    q = f"jurisdiction == '{name}'"
    data = df.query(q)
    return data.to_dict("records")




@app.get("/jurisdictions/{name}/{year}")
def get_jurisdiction_data_by_year(name :str, year:int):

    df = load_data()
    
    valid_names = df["jurisdiction"].unique()
    if name not in valid_names:
        valids = ", ".join(valid_names)
        raise HTTPException(status_code=418, detail="Wrong name. Must be one of: " + valids)
        
    valid_years = df["year"].apply(lambda x: int(x)).unique() #.astype(np.int64)
    if year not in valid_years:
        valids = ", ".join( valid_years.astype('U') )
        raise HTTPException(status_code=418, detail="Wrong year. Must be one of: " + valids)
    
    
    q = f"jurisdiction == '{name}' & year=={year}"
    data = df.query(q)
    return data.to_dict("records")




@app.get("/origins/",
    summary="list of origins",
    response_description="Array containing the origins",
)
def get_origins() -> list[str]:
    df = load_data()
    jur = df["origin"].unique() 
    return  jur ;










def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


#use_route_names_as_operation_ids(app)
