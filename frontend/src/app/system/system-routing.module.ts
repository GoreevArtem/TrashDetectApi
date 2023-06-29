import {NgModule} from "@angular/core";
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from "../shared/guards/auth.guard";
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
          {path:'load-file', component: LoadFileComponent, canActivate: [AuthGuard]},
          {path:'check', component: CheckComponent, canActivate: [AuthGuard]},
          {path:'result', component: ResultComponent, canActivate: [AuthGuard]},
        ]},
        {path:'instruction', component: InstructionComponent,canActivate: [AuthGuard]},
        {path:'contacts', component:ContactsComponent,canActivate: [AuthGuard]},
        {path:'no-photo', component:NoPhotoComponent,canActivate: [AuthGuard]},
        { path: 'account', component: AccountComponent, children: [
          {path:'personal-area', component: PersonalAreaComponent,canActivate: [AuthGuard]},
          {path:'applications', component: ApplicationsComponent,canActivate: [AuthGuard] },
          {path:'card', component: CardComponent,canActivate: [AuthGuard]}
          ]}
      ]},
     
  ]

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  
  export class SystemRoutingModule { }