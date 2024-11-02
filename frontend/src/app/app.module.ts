import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SplashScreenComponent } from './splash-screen/splash-screen.component';
import { FormsModule } from '@angular/forms';
import { AzureMapsModule } from 'ng-azure-maps';
import { environment } from '../environments/environment';
import * as atlas from 'azure-maps-control';
import { NgSelectModule } from '@ng-select/ng-select';
import { CommonModule } from '@angular/common';
import { CultivoRecomendadoComponent } from './cultivo-recomendado/cultivo-recomendado.component';
import { CultivosComponent } from './cultivos/cultivos.component';
import { CalendarModule } from 'primeng/calendar';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LoadingComponent } from './loading/loading.component';

@NgModule({
  declarations: [
    AppComponent,
    SplashScreenComponent,
    CultivoRecomendadoComponent,
    CultivosComponent,
    LoadingComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    FormsModule,
    CommonModule,
    AzureMapsModule.forRoot({
      authOptions: {
        authType: atlas.AuthenticationType.subscriptionKey,
        subscriptionKey: environment.azureMapsKey
      }
    }),
    NgSelectModule,
    CalendarModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
