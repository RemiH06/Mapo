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

estado_df <- read_csv("estados.csv")
estado_claves <- setNames(estado_df$clave, estado_df$estado)

indicador_df <- read_csv("indicadores.csv")
indicador_ids <- setNames(indicador_df$id, indicador_df$nombre)

ui <- fluidPage(
  titlePanel("Dashboard INEGI - Indicador Ejemplo"),
  sidebarLayout(
    sidebarPanel(
      selectInput("indicador_id", "Selecciona un indicador:", choices = indicador_ids),
      selectInput("estado", "Selecciona un estado:", choices = estado_claves, selected = "0700"),
      checkboxInput("recientes", "Mostrar datos recientes", value = FALSE),
      checkboxInput("usar_bie", "Usar BIE en lugar de BISE", value = FALSE)
    ),
    mainPanel(
      DTOutput("data_table")
    )
  )
)

server <- function(input, output, session) {
  token <- get_token()
  
  data_raw <- reactive({
    url <- glue(
      "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/",
      "{input$indicador_id}/es/{input$estado}/{tolower(as.character(input$recientes))}/",
      "{if (input$usar_bie) 'BIE' else 'BISE'}/2.0/{token}?type=json"
    )
    
    res <- httr::GET(url)
    req_status <- httr::status_code(res)
    
    if (req_status != 200) {
      showNotification(paste("Error al obtener datos del INEGI:", req_status), type = "error")
      return(NULL)
    }
    
    content <- httr::content(res, as = "text", encoding = "UTF-8") %>%
      jsonlite::fromJSON(flatten = TRUE)
    
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
