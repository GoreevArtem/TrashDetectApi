import {NgModule} from "@angular/core";
import { Routes, RouterModule } from '@angular/router';
import { ExpertComponent } from "./expert.component";
import { RequestComponent } from "./request/request.component";
import { RequestsComponent } from "./requests/requests.component";

const routes: Routes = [ { path: 'expert', component: ExpertComponent, children: [
  {path:'requests', component: RequestsComponent},
  {path:'request', component: RequestComponent},
  ]}
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })

  export class ExpertRoutingModule { }