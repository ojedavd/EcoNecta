import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-cultivo-recomendado',
  templateUrl: './cultivo-recomendado.component.html',
  styleUrls: ['./cultivo-recomendado.component.css']
})
export class CultivoRecomendadoComponent {
  @Input() cultivo!: { nombre: string, porcentaje: number, temperatura: string, humedad: string, lluvia: string, riego: string, tiempoCosecha: number };
}
