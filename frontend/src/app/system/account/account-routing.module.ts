import {NgModule} from "@angular/core";
import { Routes, RouterModule } from '@angular/router';
import { AccountComponent } from "./account.component";
import { ApplicationsComponent } from "./applications/applications.component";
import { CardComponent } from "./card/card.component";
import { PersonalAreaComponent } from "./personal-area/personal-area.component";

const routes: Routes = [ { path: 'account', component: AccountComponent, children: [
  {path:'personal-area', component: PersonalAreaComponent },
  {path:'applications', component: ApplicationsComponent },
  {path:'card', component: CardComponent }
  ]}
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })

  export class AccountRoutingModule { }