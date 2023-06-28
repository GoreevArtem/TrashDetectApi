import {NgModule} from "@angular/core";
import { Routes, RouterModule } from '@angular/router';
import { CheckComponent } from "./check/check.component";
import { LoadFileComponent } from "./load-file/load-file.component";
import { ResultComponent } from "./result/result.component";
import { SearchTrashComponent } from "./search-trash.component";


const routes: Routes = [
  { path: 'search-trash', component: SearchTrashComponent, children: [
      {path:'load-file', component: LoadFileComponent },
      {path:'check', component: CheckComponent},
      {path:'result', component: ResultComponent},
    ]}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class SearchTrashRoutingModule { }
