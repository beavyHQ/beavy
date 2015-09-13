import React from "react";
import { RouteHandler } from "react-router";
import { MainMenu } from "components/MainMenu";
import { createContainer } from "items-store";

class Application extends React.Component {
    static getProps(stores, params) {
        return {}
    }

    render() {
        return <div>
                    <MainMenu logo='http://svgporn.com/logos/kong.svg'/>
                    <RouteHandler />
                </div>;
    }
}

Application.contextTypes = {
    stores: React.PropTypes.object
};


export default createContainer(Application);