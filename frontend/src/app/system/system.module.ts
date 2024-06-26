import {NgModule} from "@angular/core";
import {CommonModule} from "@angular/common";
import {SystemComponent} from "./system.component";
import { SystemRoutingModule } from "./system-routing.module";
import { AboutUsComponent } from './about-us/about-us.component';
import { HeaderComponent } from './shared/components/header/header.component';
import { ContactsComponent } from './contacts/contacts.component';
import { SearchTrashModule } from "./search-trash/search-trash.module";
import { InstructionComponent } from './instruction/instruction.component';
import { NoPhotoComponent } from './no-photo/no-photo.component';
import { FormsModule } from '@angular/forms';
import { FooterComponent } from './shared/components/footer/footer.component';
import { AccountModule } from "./account/account.module";
import { RequestUserService } from "../shared/services/requestUser.service";

@NgModule({
  imports: [
    CommonModule,
    SystemRoutingModule,
    SearchTrashModule,
    FormsModule,
    AccountModule,
  ],

  declarations: [
    SystemComponent,
    AboutUsComponent,
    HeaderComponent,
    ContactsComponent,
    InstructionComponent,
    NoPhotoComponent,
    FooterComponent,
  ],
  providers:[RequestUserService]
})
export class SystemModule { }
