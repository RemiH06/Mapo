library(httr)
library(jsonlite)
library(magrittr)  # para %>%

# Leer token
secrets <- fromJSON(".secrets")
token <- secrets$token
print(paste("Token leído:", token))

# Construir URL
url <- paste0(
  "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/",
  "1002000041/es/0700/false/BISE/2.0/", token, "?type=json"
)

# Hacer consulta
response <- GET(url)

# Revisar status
print(paste("Status code:", status_code(response)))

if (status_code(response) == 200) {
  data <- content(response, "text", encoding = "UTF-8") %>%
    fromJSON(flatten = TRUE)
  print("Consulta exitosa, ejemplo de datos:")
  print(head(data))
} else {
  print("Error en la consulta. Revisa token o permisos.")
}

