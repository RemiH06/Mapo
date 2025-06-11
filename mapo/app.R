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

# Cargar el archivo CSV subido para obtener la estructura de los indicadores
indicador_df <- read.csv("indicadores.csv", fileEncoding = "ISO-8859-1")
indicador_ids <- setNames(indicador_df$id, indicador_df$nombre)

# Función para obtener las opciones de filtros (bdi, sect, clase, subclase, infraclase)
get_filters <- function(bdi, sect = NULL, clase = NULL, subclase = NULL) {
  df <- indicador_df %>% filter(bdi == bdi)
  
  if (!is.null(sect)) {
    df <- df %>% filter(sect == sect)
  }
  if (!is.null(clase)) {
    df <- df %>% filter(clase == clase)
  }
  if (!is.null(subclase)) {
    df <- df %>% filter(subclase == subclase)
  }
  
  # Filtrar los valores posibles para cada uno de los campos
  sects <- unique(df$sect)
  clases <- unique(df$clase)
  subclases <- unique(df$subclase)
  infraclases <- unique(df$infraclase)
  
  list(sects = sects, clases = clases, subclases = subclases, infraclases = infraclases)
}

ui <- fluidPage(
  titlePanel("Dashboard INEGI - Indicador Ejemplo"),
  sidebarLayout(
    sidebarPanel(
      selectInput("indicador_id", "Selecciona un indicador:", choices = indicador_ids),
      selectInput("estado", "Selecciona un estado:", choices = estado_claves, selected = "0700"),
      checkboxInput("recientes", "Mostrar datos recientes", value = FALSE),
      checkboxInput("usar_bie", "Usar BIE en lugar de BISE", value = FALSE),
      
      # Selector de BDI
      selectInput("bdi", "Selecciona BDI:", choices = c("BIE", "BISE")),
      
      # Selector de Sectores
      uiOutput("sect_ui"),
      
      # Selector de Clase
      uiOutput("clase_ui"),
      
      # Selector de Subclase
      uiOutput("subclase_ui"),
      
      # Selector de infraclase
      uiOutput("infraclase_ui")
    ),
    mainPanel(
      DTOutput("data_table"),
      verbatimTextOutput("consulta_texto")  # Mostrar consultas posibles
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
  
  # Generar el UI de Sectores dependiendo de la selección de BDI
  output$sect_ui <- renderUI({
    req(input$bdi)
    filters <- get_filters(input$bdi)
    selectInput("sect", "Selecciona un sector:", choices = filters$sects)
  })
  
  # Generar el UI de Clases dependiendo de la selección de Sector
  output$clase_ui <- renderUI({
    req(input$sect)
    filters <- get_filters(input$bdi, sect = input$sect)
    selectInput("clase", "Selecciona una clase:", choices = filters$clases)
  })
  
  # Generar el UI de Subclases dependiendo de la selección de Clase
  output$subclase_ui <- renderUI({
    req(input$clase)
    filters <- get_filters(input$bdi, sect = input$sect, clase = input$clase)
    selectInput("subclase", "Selecciona una subclase:", choices = filters$subclases)
  })
  
  # Generar el UI de infraclases dependiendo de la selección de Subclase
  output$infraclase_ui <- renderUI({
    req(input$subclase)
    filters <- get_filters(input$bdi, sect = input$sect, clase = input$clase, subclase = input$subclase)
    selectInput("infraclase", "Selecciona una infraclase:", choices = filters$infraclases)
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
  
  output$consulta_texto <- renderText({
    paste("Consultas posibles con los filtros elegidos:",
          "\nBDI: ", input$bdi,
          "\nSector: ", input$sect,
          "\nClase: ", input$clase,
          "\nSubclase: ", input$subclase,
          "\nInfraclase: ", input$infraclase)
  })
}

shinyApp(ui, server)
