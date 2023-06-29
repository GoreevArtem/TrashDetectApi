import {NgModule} from "@angular/core";
import {CommonModule} from "@angular/common";
import { SearchTrashComponent } from "./search-trash.component";
import { SearchTrashRoutingModule } from "./search-tarsh-routing.module";
import { CheckComponent } from "./check/check.component";
import { LoadFileComponent } from "./load-file/load-file.component";
import { BrowserModule } from "@angular/platform-browser";
import { YandexMapService } from "../../shared/services/yandex-map_service";
import { HttpClientModule } from "@angular/common/http";
import { FormsModule } from '@angular/forms';
import { ResultComponent } from "./result/result.component";
import { PhotoService } from "src/app/shared/services/photo.service";

@NgModule({
  imports: [
    CommonModule,
    BrowserModule,
    SearchTrashRoutingModule,
    HttpClientModule,
    FormsModule
  ],

  declarations: [
    SearchTrashComponent,
    CheckComponent,
    LoadFileComponent,
    ResultComponent
  ],
  providers:[YandexMapService,PhotoService]
})
export class SearchTrashModule{ }
