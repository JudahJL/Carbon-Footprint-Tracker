from pydantic import BaseModel, Field
from typing import Optional, Annotated

type CO2PerYear = Annotated[float, Field(description="Carbon emissions in kilograms (kg) of CO₂ per year.")]
type Reason = Annotated[str, Field(description="Justification or explanation for the emission value.")]


class EmissionDetail(BaseModel):
    value: CO2PerYear
    reason: Reason


class CarbonFootprintResponse(BaseModel):
    transportation: Annotated[Optional[EmissionDetail], Field(description="Annual emissions from transportation (cars, flights, etc.) in kg CO₂/year and the reason.")]
    energy: Annotated[Optional[EmissionDetail], Field(description="Estimated annual carbon emissions from household energy consumption (e.g., electricity, heating, cooling), with an explanation.")]
    diet: Annotated[Optional[EmissionDetail], Field(description="Annual carbon footprint related to food consumption (e.g., dietary choices, food sourcing), with reasoning.")]
    other: Annotated[Optional[EmissionDetail], Field(description="Annual carbon emissions from other unaccounted-for activities (e.g., shopping, services, entertainment), along with an explanation.")]
    total_emissions: Annotated[Optional[EmissionDetail], Field(description="Total estimated annual carbon emissions across all categories (kg CO₂/year), along with a summary explanation. Required if any subcategory is provided.")]
    recommendations: Annotated[Optional[str], Field(description="Recommendations or strategies to reduce carbon emissions based on the provided data.")]
    valid_data_provided: Annotated[bool, Field(description="Indicates whether the provided data is relevant for assessing carbon footprint. Set to true if at least one emission category contains meaningful information.")]
