import React from "react";
import { MainMenu } from "components/MainMenu";
import { connect } from 'react-redux';


import styles from "./styles/twitterApp.scss";


export default class Application extends React.Component {
    static getProps(stores, params) {
        var transition = stores.Router.getItem("transition");
        return {
            loading: !!transition
        };
    }
    render() {
        var { loading } = this.props;
        return <div className={styles.this + (loading ? " " + styles.loading : "")}>
            <div className={styles.loadingElement}>loading...</div>
            <MainMenu logo='http://svgporn.com/logos/twitter.svg'/>
            <h1>Twitter</h1>
            {this.props.children}
        </div>;
    }
};
