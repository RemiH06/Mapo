library(shiny)
library(httr)
library(jsonlite)
library(tidyverse)
library(DT)
library(glue)

get_token <- function() {
  secrets <- jsonlite::fromJSON("../.secrets")
  secrets$token
}

ui <- fluidPage(
  titlePanel("Dashboard INEGI - Indicador Ejemplo"),
  mainPanel(
    DTOutput("data_table")
  )
)

server <- function(input, output, session) {
  token <- get_token()
  
  url <- glue(
    "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/",
    "1002000041/es/0700/false/BISE/2.0/{token}?type=json"
  )
  
  data_raw <- reactive({
    res <- httr::GET(url)
    req_status <- httr::status_code(res)
    
    if (req_status != 200) {
      showNotification(paste("Error al obtener datos del INEGI:", req_status), type = "error")
      return(NULL)
    }
    
    content <- httr::content(res, as = "text", encoding = "UTF-8") %>%
      jsonlite::fromJSON(flatten = TRUE)
    
    # Imprime en consola la estructura para revisión
    print(str(content, max.level = 3))
    
    content
  })
  
  
  output$data_table <- renderDT({
    data <- data_raw()
    req(!is.null(data))
    
    dat <- data %>%
      purrr::pluck("Series", "OBSERVATIONS", 1) %>%
      as_tibble()
    
    if (nrow(dat) == 0) {
      return(tibble(Mensaje = "No se encontraron observaciones"))
    }
    
    dat %>% datatable()
  })
  
}

shinyApp(ui, server)
