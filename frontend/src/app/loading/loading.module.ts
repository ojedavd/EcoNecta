import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoadingComponent } from './loading.component';
import { LoadingController } from './loading.controller';

@NgModule({
  declarations: [
    LoadingComponent,
  ],
  imports: [
    CommonModule,
  ],
  providers: [
    LoadingController,
  ],
  exports: [
    LoadingComponent,
  ],
})
export class LoadingModule { }
