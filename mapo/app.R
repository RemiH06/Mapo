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

# Lista de claves de estado
estado_claves <- c(
  "Aguascalientes" = "07000001",
  "Baja California" = "07000002",
  "Baja California Sur" = "07000003",
  "Campeche" = "07000004",
  "Coahuila" = "07000005",
  "Colima" = "07000006",
  "Chiapas" = "07000007",
  "Chihuahua" = "07000008",
  "Ciudad de México" = "07000009",
  "Durango" = "07000010",
  "Guanajuato" = "07000011",
  "Guerrero" = "07000012",
  "Hidalgo" = "07000013",
  "Jalisco" = "07000014",
  "México" = "07000015",
  "Michoacán" = "07000016",
  "Morelos" = "07000017",
  "Nayarit" = "07000018",
  "Nuevo León" = "07000019",
  "Oaxaca" = "07000020",
  "Puebla" = "07000021",
  "Querétaro" = "07000022",
  "Quintana Roo" = "07000023",
  "San Luis Potosí" = "07000024",
  "Sinaloa" = "07000025",
  "Sonora" = "07000026",
  "Tabasco" = "07000027",
  "Tamaulipas" = "07000028",
  "Tlaxcala" = "07000029",
  "Veracruz" = "07000030",
  "Yucatán" = "07000031",
  "Zacatecas" = "07000032",
  "Toda la República" = "0700"
)

ui <- fluidPage(
  titlePanel("Dashboard INEGI - Indicador Ejemplo"),
  sidebarLayout(
    sidebarPanel(
      selectInput("estado", "Selecciona un estado:",
                  choices = estado_claves,
                  selected = "0700")
    ),
    mainPanel(
      DTOutput("data_table")
    )
  )
)

server <- function(input, output, session) {
  token <- get_token()
  
  data_raw <- reactive({
    clave_estado <- input$estado
    
    url <- glue(
      "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/",
      "1002000041/es/{clave_estado}/false/BISE/2.0/{token}?type=json"
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
