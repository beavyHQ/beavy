import React from "react";
import { Link } from "react-router";
import ReactLogo from "elements/ReactLogo";
import styles from './MainMenu.scss';
import classnames from 'classnames';

var MenuItems = []

export function registerMainMenuItem(item){
	console.log(item)
	MenuItems.push(item);
}

export class MainMenu extends React.Component {
	render() {
		return <div className={styles.navigation} role="banner">
			  <div className={styles.navigationWrapper}>
			    <a href="javascript:void(0)" className="logo">
			      <img src="https://raw.githubusercontent.com/thoughtbot/refills/master/source/images/placeholder_logo_1.png" alt="Logo Image" />
			    </a>
			    <a href="javascript:void(0)" className={styles.navigationMenuButton} id="js-mobile-menu">MENU</a>
			    <nav role="navigation">
			      <ul id="js-navigation-menu" className={classnames(styles.navigationMenu, styles.show)}>
			      	{MenuItems.map(x=>x.apply(this))}
			        <li><a href="javascript:void(0)">Products</a></li>
			        <li><a href="javascript:void(0)">About Us</a></li>
			        <li><a href="javascript:void(0)">Contact</a></li>
			        <li className={styles.more}><a href="javascript:void(0)">More</a>
			          <ul className={styles.submenu}>
			            <li><a href="javascript:void(0)">Submenu Item</a></li>
			            <li><a href="javascript:void(0)">Another Item</a></li>
			            <li className={styles.more}><a href="javascript:void(0)">Item with submenu</a>
			              <ul className={styles.submenu}>
			                <li><a href="javascript:void(0)">Sub-submenu Item</a></li>
			                <li><a href="javascript:void(0)">Another Item</a></li>
			              </ul>
			            </li>
			            <li className={styles.more}><a href="javascript:void(0)">Another submenu</a>
			              <ul className={styles.submenu}>
			                <li><a href="javascript:void(0)">Sub-submenu</a></li>
			                <li><a href="javascript:void(0)">An Item</a></li>
			              </ul>
			            </li>
			          </ul>
			        </li>
			      </ul>
			    </nav>
			    <div className={styles.navigationTools}>
			      <div className={styles.searchBar}>
			        <form role="search">
			          <input type="search" placeholder="Enter Search" />
			          <button type="submit">
			            <img src="https://raw.githubusercontent.com/thoughtbot/refills/master/source/images/search-icon.png" alt="Search Icon" />
			          </button>
			        </form>
			      </div>
			    </div>
			  </div>
		</div>;
	}
}
