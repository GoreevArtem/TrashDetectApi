import {NgModule} from "@angular/core";
import { Routes, RouterModule } from '@angular/router';
import { AboutUsComponent } from "./about-us/about-us.component";
import { AccountComponent } from "./account/account.component";
import { ApplicationsComponent } from "./account/applications/applications.component";
import { CardComponent } from "./account/card/card.component";
import { PersonalAreaComponent } from "./account/personal-area/personal-area.component";
import { ContactsComponent } from "./contacts/contacts.component";
import { InstructionComponent } from "./instruction/instruction.component";
import { NoPhotoComponent } from "./no-photo/no-photo.component";
import { CheckComponent } from "./search-trash/check/check.component";
import { LoadFileComponent } from "./search-trash/load-file/load-file.component";
import { ResultComponent } from "./search-trash/result/result.component";
import { SearchTrashComponent } from "./search-trash/search-trash.component";
import {SystemComponent} from "./system.component";

const routes: Routes = [
    { path: 'system', component: SystemComponent,  children: [
        {path:'about-us', component:AboutUsComponent},
        {path:'search-trash', component:SearchTrashComponent, children: [
          {path:'load-file', component: LoadFileComponent },
          {path:'check', component: CheckComponent},
          {path:'result', component: ResultComponent},
        ]},
        {path:'instruction', component: InstructionComponent},
        {path:'contacts', component:ContactsComponent},
        {path:'no-photo', component:NoPhotoComponent},
        { path: 'account', component: AccountComponent, children: [
          {path:'personal-area', component: PersonalAreaComponent},
          {path:'applications', component: ApplicationsComponent },
          {path:'card', component: CardComponent }
          ]}
      ]},
     
  ]

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  
  export class SystemRoutingModule { }