import { EnvironmentPlugin } from 'webpack';
require('dotenv').config()

module.exports={
    plugins:[
        new EnvironmentPlugin(["API"])
    ]
}