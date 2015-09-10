import React from "react";
import { Link } from "react-router";
import {registerMainMenuItem} from './../../app/components/MainMenu.jsx';

console.log(registerMainMenuItem)

registerMainMenuItem(function() {
  return (<li><Link to="home">other</Link> this comes from comments</li>)
});