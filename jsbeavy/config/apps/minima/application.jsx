import React from "react";
import { MainMenu } from "components/MainMenu";

export default class Application extends React.Component {
    render() {
        return <div>
                    <MainMenu logo='http://svgporn.com/logos/kong.svg'/>
                    {this.props.children}
                </div>;
    }
}
