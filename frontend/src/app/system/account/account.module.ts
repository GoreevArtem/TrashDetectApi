import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { BrowserModule } from "@angular/platform-browser";
import { HttpClientModule } from "@angular/common/http";
import { AccountRoutingModule } from "./account-routing.module";
import { AccountComponent } from "./account.component";
import { PersonalAreaComponent } from './personal-area/personal-area.component';
import { MenuAccountComponent } from './shared/components/menu-account/menu-account.component';
import { ApplicationsComponent } from './applications/applications.component';
import { CardComponent } from './card/card.component';
import { UserService } from "src/app/shared/services/user.service";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { SearchPipe } from './search.pipe';
import { YandexMapService } from "../../shared/services/yandex-map_service";
import { RequestUserService } from "src/app/shared/services/requestUser.service";


@NgModule({
    imports: [
        CommonModule,
        BrowserModule,
        HttpClientModule,
        AccountRoutingModule,
        FormsModule,
        ReactiveFormsModule
    ],

    declarations: [
        AccountComponent,
        PersonalAreaComponent,
        MenuAccountComponent,
        ApplicationsComponent,
        CardComponent,
        SearchPipe

    ],
    providers: [YandexMapService, UserService, RequestUserService]
})
export class AccountModule { }
