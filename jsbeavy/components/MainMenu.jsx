import React from "react";
import { Link } from "react-router";
import ReactLogo from "elements/ReactLogo";
import styles from './MainMenu.scss';
import classnames from 'classnames';

let MainMenuItems = []
let NavigationTools = []

export var registerMainMenuItem = i => MainMenuItems.push(i);
export var registerNavigationToolsItem = i => NavigationTools.push(i);

export class MainMenu extends React.Component {
	render() {
		let logo = this.props.logo || 'https://raw.githubusercontent.com/thoughtbot/refills/master/source/images/placeholder_logo_1.png'
		return <div className={styles.navigation} role="banner">
			  <div className={styles.navigationWrapper}>
			    <Link to="app" className={styles.logo}>
			      <img src={logo} alt="Logo Image" />
			    </Link>
			    <a href="" className={styles.navigationMenuButton} id="js-mobile-menu">MENU</a>
			    <nav role="navigation">
			      <ul id="js-navigation-menu" className={classnames(styles.navigationMenu, styles.show)}>
			      	{MainMenuItems.map(x=>x.apply(this))}
			      </ul>
			    </nav>
			    <div className={styles.navigationTools}>
			    	{NavigationTools.map(x=>x.apply(this))}
			    </div>
			  </div>
		</div>;
	}
}
