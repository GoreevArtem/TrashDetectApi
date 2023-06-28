import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { environment } from "src/app/environment";
import { JWT_NAME } from "./auth.service";

@Injectable()
export class UserService {
    constructor(private http: HttpClient){}
    private path1='user/me';
    private path2='user/me_delete';
    private path3='user/update_password';
    private path4='user/update_email';

    getUser()
    {
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${ localStorage.getItem(JWT_NAME)}`})}; 
        return this.http.get<any>(`${environment.api}${this.path1}`,httpOptions);
    }

    deleteUser()
    {
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${localStorage.getItem(JWT_NAME)}`})}; 
        return this.http.delete<any>(`${environment.api}${this.path2}`,httpOptions);
    }

    updatePassword(data:any)
    {
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${localStorage.getItem(JWT_NAME)}`})}; 
        return this.http.patch(`${environment.api}${this.path3}`,data,httpOptions);
    }

    updateLogin(data:any)
    {
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${localStorage.getItem(JWT_NAME)}`})}; 
        return this.http.patch(`${environment.api}${this.path4}`,data,httpOptions);
    }
}