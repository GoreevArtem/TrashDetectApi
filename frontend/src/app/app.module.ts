import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthModule } from './auth/auth.module';
import { SystemModule } from './system/system.module';
import { ExpertModule } from './expert/expert.module';
import { AuthService } from './shared/services/auth.service';


@NgModule({
  declarations: [
    AppComponent,
    ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AuthModule,
    HttpClientModule,
    SystemModule,
    ExpertModule
  ],
  providers: [AuthService],
  bootstrap: [AppComponent]
})
export class AppModule { }
