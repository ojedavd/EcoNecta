import { Component, AfterViewInit } from '@angular/core';
import * as atlas from 'azure-maps-control';
import Swal from 'sweetalert2';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements AfterViewInit {
  title = 'ng-azure-maps-tutorial';
  staging: 'starting' | 'loading' | 'show-results' = 'starting';
  map!: atlas.Map;
  currentMarker: atlas.HtmlMarker | null = null;
  currentDataSource: atlas.source.DataSource | null = null;
  currentLayer: atlas.layer.PolygonLayer | null = null;

  tipoCultivo!: string;
  fecha!: string;
  coordenadas: [number, number] | null = null;
  cultivos = [
    { name: 'Maíz', value: 'maiz' },
    { name: 'Trigo', value: 'trigo' },
    { name: 'Soja', value: 'soja' }
    // Agrega más opciones según sea necesario
  ];

  constructor(private http: HttpClient) {}

  ngAfterViewInit() {
    this.map = new atlas.Map('myMap', {
      center: [0, 0],
      zoom: 13
    });

    // Obtener la ubicación actual del usuario
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(position => {
        const userLocation = [position.coords.longitude, position.coords.latitude];

        // Centrar y hacer zoom en la ubicación del usuario
        this.map.setCamera({
          // center: userLocation,
          center: [-66.34215140649547, -17.349436321389078],
          zoom: 13 // Puedes ajustar el nivel de zoom según tus necesidades
        });
      });
    } else {
      console.error("Geolocalización no es soportada por este navegador.");
    }

    // Agregar el controlador de eventos de clic de Azure Maps
    this.map.events.add('click', (event: atlas.MapMouseEvent) => this.mapClick(event));
  }

  mapClick(event: atlas.MapMouseEvent) {
    console.log(event.position);

    this.removeCurrentMarkerAndCircle();
    this.addNewMarker(event.position!);
    this.drawCircle(event.position!);
    this.coordenadas = event.position as [number, number];

    // Fetch weather data for the clicked location
    this.getWeatherData(this.coordenadas);
  }

  private removeCurrentMarkerAndCircle() {
    // Eliminar el marcador actual si existe
    if (this.currentMarker) {
      this.map.markers.remove(this.currentMarker);
      this.currentMarker = null;
    }

    // Eliminar la capa y la fuente de datos actuales si existen
    if (this.currentLayer && this.currentDataSource) {
      this.map.layers.remove(this.currentLayer);
      this.map.sources.remove(this.currentDataSource);
      this.currentLayer = null;
      this.currentDataSource = null;
    }
  }

  private addNewMarker(position: atlas.data.Position) {
    // Agregar un nuevo marcador en la posición del clic
    const marker = new atlas.HtmlMarker({
      position: position
    });

    this.map.markers.add(marker);
    this.currentMarker = marker;
  }

  private drawCircle(position: atlas.data.Position) {
    // Crear una fuente de datos y agregarla al mapa
    const dataSource = new atlas.source.DataSource();
    this.map.sources.add(dataSource);

    // Crear un círculo
    dataSource.add(new atlas.data.Feature(new atlas.data.Point([position[0], position[1]]), {
      subType: "Circle",
      radius: 700
    }));

    // Crear una capa de polígono para renderizar el área del círculo y agregarla al mapa
    const layer = new atlas.layer.PolygonLayer(dataSource, undefined, {
      fillColor: 'rgba(0, 200, 200, 0.8)'
    });
    this.map.layers.add(layer);

    this.currentDataSource = dataSource;
    this.currentLayer = layer;
  }

  getWeatherData(coordinates: [number, number]) {
    // const url = `https://atlas.microsoft.com/weather/currentConditions/json?api-version=1.0&query=${coordinates[1]},${coordinates[0]}`;
    const url = `https://atlas.microsoft.com/search/address/reverse/json?&api-version=1.0&query=${coordinates[1]},${coordinates[0]}&language=es-ES`;

    this.http.get(url).subscribe((data: any) => {
      console.log('Weather data:', data);
      const {country, countrySubdivision, localName, street} = data.addresses[0].address
      // Swal.fire({
      //   title: 'Dirección',
      //   text: `${street}, ${localName}, ${countrySubdivision}, ${country}`,
      //   icon: 'info',
      //   confirmButtonText: 'OK'
      // });
    });
  }

  onSubmit() {
    const datos = {
      tipoCultivo: this.tipoCultivo,
      fecha: this.fecha,
      coordenadas: this.coordenadas
    };
    console.log('Datos enviados:', datos);

    // Swal.fire({
    //   title: 'Datos enviados',
    //   text: `Los datos se enviaron correctamente`,
    //   icon: 'success',
    //   confirmButtonText: 'OK'
    // });

    this.staging = 'loading';

    // lamada a backend
    setTimeout(()=>{
      this.staging = 'show-results';
    },2000);


  }


}
