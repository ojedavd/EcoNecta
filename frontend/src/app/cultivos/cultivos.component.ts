import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-cultivos',
  templateUrl: './cultivos.component.html',
  styleUrls: ['./cultivos.component.css']
})
export class CultivosComponent implements OnInit {
  cultivos = [
    { nombre: 'Maíz', porcentaje: 92, 'temperatura': '12°', 'humedad': '7%', 'lluvia': '4mm', riego: 'Moderado', tiempoCosecha: 120 },
    { nombre: 'Trigo', porcentaje: 85, 'temperatura': '22°', 'humedad': '3%', 'lluvia': '30mm', riego: 'Bajo', tiempoCosecha: 110 },
    { nombre: 'Arroz', porcentaje: 78, 'temperatura': '33°', 'humedad': '1%', 'lluvia': '12mm', riego: 'Alto', tiempoCosecha: 150 },
    // Agrega más cultivos según sea necesario
  ];

  ngOnInit(): void {
    // Aquí puedes cargar los datos desde un servicio en un proyecto real
  }
}
