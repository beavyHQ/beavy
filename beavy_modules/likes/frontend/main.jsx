import React from "react";
import { Link } from "react-router";
import { addExtension } from 'config/extensions';


addExtension("MainMenuItem", function() {
  return (<li><Link to="home">home</Link>Test</li>)
});