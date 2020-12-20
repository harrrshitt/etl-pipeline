
## Dashboard Dependencies and Pipeline Description (Draft)

|               Graph               |  Sheets used  |        Columns used       | Documented |
|:---------------------------------:|:-------------:|:-------------------------:|:----------:|
|           City dropdown           |    metrics    |          district         |     n/a    |
|            Date slicer            |    metrics    |            date           |     n/a    |
|           Summary stats           |    metrics    |      delta.confirmed      |     n/a    |
|           Summary stats           |    metrics    |       delta.deceased      |     n/a    |
|           Summary stats           |    metrics    |        delta.tested       |     n/a    |
|           Summary stats           |    metrics    |      delta.recovered      |     n/a    |
|           Summary stats           |    metrics    |            date           |     n/a    |
|           Summary stats           |    metrics    |     delta.hospitalized    |     n/a    |
| Case growth rate and active cases |    metrics    | delta.percent.case.growth |     n/a    |
| Case growth rate and active cases |    metrics    |       spline.active       |     n/a    |
|             Fatalities            |    metrics    |       delta.deceased      |     n/a    |
|             Fatalities            |    metrics    |      spline.deceased      |     n/a    |
|             Fatalities            |    metrics    |            date           |     n/a    |
|               Tests               |    metrics    |        delta.tested       |     n/a    |
|               Tests               |    metrics    |            date           |     n/a    |
|               Tests               |    metrics    |     MA.21.daily.tests     |     n/a    |
|          Hospitalizations         |    metrics    |            date           |     n/a    |
|          Hospitalizations         |    metrics    |     delta.hospitalized    |     n/a    |
|          Hospitalizations         |    metrics    |    spline.hospitalized    |     n/a    |
|             Recoveries            |    metrics    |            date           |     n/a    |
|             Recoveries            |    metrics    |      delta.recovered      |     n/a    |
|             Recoveries            |    metrics    |      spline.recovered     |     n/a    |
|        Test positivity rate       |    metrics    |            date           |     n/a    |
|        Test positivity rate       |    metrics    |   MA.21.delta.positivity  |     n/a    |
|        Test positivity rate       |    metrics    |      delta.positivity     |     n/a    |
|         Reproduction rate         |       Rt      |            date           |     n/a    |
|         Reproduction rate         |       Rt      |         mean.mean         |     n/a    |
|         Reproduction rate         |       Rt      |       CI_lower.mean       |     n/a    |
|         Reproduction rate         |       Rt      |       CI_upper.mean       |     n/a    |
|           Doubling time           | doubling_time |       doubling.time       |     n/a    |
|           Doubling time           |    metrics    |      delta.confirmed      |     n/a    |
|           Doubling time           |    metrics    |            date           |     n/a    |
|           Levitt metric           |    metrics    |            date           |     n/a    |
|           Levitt metric           |    metrics    |       levitt.Metric       |     n/a    |
|------------------------------------| -------------|---------------------------|------------| 

## Dependencies 

Garima clarified that most of these sheets and columns are generated from running calculate_metrics.py


**1) calculate_metrics.py**
- Currently, the primary function, calculate_metrics(), outputs csv's to output/percentages_for_hospitalizations.csv and output/city_metrics.py
- In some of the existing docs, I am reading that calculate_metrics.py is executed as part of the CalculateCityMetricsTask; however, I don't see that task or its wrapper task, SWBPipelineWrapper (referring to the etl-pipeline/pipeline README) in any of the existing github action workflows. 
- In the data_pipeline task, `pipeline.tasks.spreadsheets AllDataGSheetTask` is run. [AllDataGSheetTask](https://github.com/swb-ief/etl-pipeline/blob/6e1096d0b170103504e68df71e4c849f2abe3188/pipeline/pipeline/tasks/spreadsheets.py#L32) is where the csv outputs of calculate_metrics.py (city_metrics.csv and percentages_for_hospitalizations.csv) are piped to Google Sheets using **new** names. 
- For example, city_metrics.csv is piped to the "metrics" Google Sheet. 



