*Diatribas*

**Diario de cambios:**

**[Remi]**
*Viernes 04/07/25 23:18 o algo así*:
<br>-> *For the sake of the workflow*
<br>-> Como normalmente no hago una documentación tan detallada para mis proyectos, no había pensado en que tendría que hacer más que el burdo pero confiable README.md
<br>-> Dejó de ser el caso, entre 7 personas inscribimos esta idea para una competencia de Intel, muchas gracias al coordinador de carrera Riemann Ruiz por compartirnos la convocatoria. 
<br>-> Con eso en mente, me gustaría dejar en claro que este markdown servirá para apreciar de mejor manera los cambios que cada quién ha hecho, no necesita ser algo muy detallado, simplemente explicar archivos modificados y qué cambios hubieron, se agradecen notas adicionales, comentarios, dudas, quejas y solicitudes de ayuda.
<br>-> Escriban como se les haga más cómodo, no es a fuerzas registrar horas (fechas preferiblemente sí), yo lo hago porque si no me da ansiedad. Por favor no modifiquen de ninguna manera logs ajenos. Gracias.
<br>

**[Remi]**
*Viernes 04/07/25 23:29*:
<br>[Docs] -> Respecto a la documentación, no la comenzaré aún porque antes quiero terminar un coso que grafica códigos postales, igual les dejo la lista de documentos que tendremos, acepto sugerencias:
<br> - PoC (prueba de concepto)
<br> - RF/RNF
<br> - Gantt
<br> - Modelado de datos
<br> - Grafo de módulos
<br> - Grafo de dependencias
<br> - Diagrama de procesos
<br> - Diccionario de datos
<br> - Manual de usuario

**[Remi]**
*Sábado 05/07/25 01:12:*
<br> [mapsDashboard.py] -> creé el file y grafica bien los polígonos (single run de pocos segundos, pero se vuelve muy lento al intentar hacer iteraciones posteriores, creo que es por el peso de los archivos, pude comprobarlo con Jalisco que es de los más pesados), requiere KMLs que si los necesitan se los paso por otro lado porque cada uno pesa entre 3 y 30 MBs (y aparte ya tengo mi estructura de archivos xd). 
<br> -> Planeo ponerle filtros para prender y apagar la visualización de estados específicos. Prolly haga un rework para guardar cada zipcode como su propio objeto en vez de tener todo ensartado cual blob field.

**[Remi]**
*Domingo 06/07/25 20:51:*
<br> [mapsDashboard.py] -> agregué filtros de estado, como no tiene que cargar todo de una sola vez, ahora es más rápido.
<br> solo se me ha ocurrido una manera de guardar cada zipcode como su propio objeto, y es con un regex, pero dada la naturaleza de los xml no tengo certeza de que pueda ser una solución general. Comenzaré con pruebas mañana.

**[Remi]**
*Jueves 17/07/25 19:12:*
<br> [Docs] -> llevo avanzando un rato en la documentación, el listado de requerimientos está bastante avanzado y eso permite el trabajo en otra clase de documentación, creo que haré un diagrama de tablas mañana.

**[Vivienne]**
*Sábado 19/07/25:*
<br> Hice una carpeta llamada [team1] con avances y archivos correspondientes en cuanto al matcheo de los AGEBs y Códigos Postales. Por ahora tiene un archivo [agebs.ipynb] con código exploratorio para los archivos .shp, muy rudimental.

**[Sofi]**
*Domingo 20/07/2025 16:34*
<br> Hice la primer versión del scrapper de los archivos esos grandes de KML. Todavía planeo hacerle lo siguiente: 
- Refinar el código para ya ponerlo en un .py y que no sea un notebook
- Ver si puedo poner las coordenadas en una lista de tuplas en vez de que sea un string enorme
- Encontrar cómo agregar la info adicional como el municipio, las colonias dentro del CP y si es un código postal urbano o rural
