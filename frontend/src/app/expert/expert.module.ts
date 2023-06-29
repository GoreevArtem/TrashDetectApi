import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { BrowserModule } from "@angular/platform-browser";
import { HttpClientModule } from "@angular/common/http";
import { ExpertComponent } from "./expert.component";
import { ExpertRoutingModule } from "./expert-routing.module";
import { RequestsComponent } from './requests/requests.component';
import { FooterComponent } from "./shared/components/footer/footer.component";
import { HeaderComponent } from "./shared/components/header/header.component";
import { RequestComponent } from './request/request.component';
import { YandexMapService } from "../shared/services/yandex-map_service";
import { ExpertService } from "../shared/services/expert.service";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { SearchExPipe } from './search-ex.pipe';
import { RequestsExService } from "../shared/services/requestsEx.service";

@NgModule({
    imports: [
        CommonModule,
        BrowserModule,
        HttpClientModule,
        ExpertRoutingModule,
        FormsModule,
        ReactiveFormsModule
    ],
    declarations: [
      ExpertComponent,
      RequestsComponent,
      FooterComponent,
      HeaderComponent,
      RequestComponent,
      SearchExPipe,
    ],
    providers: [YandexMapService,ExpertService,RequestsExService]
})
export class ExpertModule { }