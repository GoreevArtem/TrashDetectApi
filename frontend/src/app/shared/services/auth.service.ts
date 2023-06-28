import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { User } from "../model/user.model";
import { environment } from "src/app/environment";
import { JwtHelperService } from "@auth0/angular-jwt";
export const JWT_NAME = 'token';

@Injectable()
export class AuthService {
    private path1='auth/register';
    private path2='auth/authenticate';
    private path3='expert/register';
    private path4='expert/authenticate';

    constructor(private http: HttpClient, private jwtHelper: JwtHelperService){}

    signUpUser(user:User)
    {
        return this.http.post<any>(`${environment.api}${this.path1}`,user);
    }

    loginUser(user: User)
    {
        return this.http.post<any>(`${environment.api}${this.path2}`,user);
    }

    signUpExpert(expert: any)
    {
        return this.http.post<any>(`${environment.api}${this.path3}`,expert);
    }

    loginExpert(expert: any)
    {
        return this.http.post<any>(`${environment.api}${this.path4}`,expert);
    }
   
    isAuthenticated(): boolean {
        const token = localStorage.getItem(JWT_NAME);
        return !this.jwtHelper.isTokenExpired(token);
    }
        
}