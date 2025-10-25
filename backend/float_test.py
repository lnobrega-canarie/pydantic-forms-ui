from typing import Annotated, ClassVar
from annotated_types import Ge, Le, MultipleOf

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import ConfigDict
from pydantic_forms.core import post_form
from pydantic_forms.types import State
from pydantic_forms.exception_handlers.fastapi import form_error_handler
from pydantic_forms.exceptions import FormException
from pydantic_forms.core import FormPage as PydanticFormsFormPage
from pydantic_forms.types import JSON


class FormPage(PydanticFormsFormPage):
    meta__: ClassVar[JSON] = {"hasNext": True}


app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.add_exception_handler(
    FormException,
    form_error_handler
)  # type: ignore[arg-type]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/form")
async def form(form_data: list[dict] = []):
    def form_generator(state: State):

        class TestForm(FormPage):
            model_config = ConfigDict(title="Float test form")
            unrestricted_float_value: float
            float_range_value: Annotated[float, Ge(-90.0), Le(90.0)]
            two_decimals_float_value: Annotated[
                float,
                MultipleOf(multiple_of=0.01),
            ]

        test_form_data = yield TestForm
        return test_form_data.model_dump()

    post_form(form_generator, state={}, user_inputs=form_data)
    return "OK!"
