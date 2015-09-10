import React from "react";
import { Link } from "react-router";
import ReactLogo from "elements/ReactLogo";

var MenuItems = []

export function registerMainMenuItem(item){
	console.log(item)
	MenuItems.push(item);
}

export class MainMenu extends React.Component {
	render() {
		return <div>
			<ReactLogo type="svg" /> <ReactLogo type="png" /> <ReactLogo type="jpg" />
			<h2>MainMenu:</h2>
			<ul>
				<li>The <Link to="home">home</Link> page.</li>
				<li>Switch to <Link to="some-page">some page</Link>.</li>
				<li>Open the page that shows <Link to="readme">README.md</Link>.</li>
				{MenuItems.map(x=>x.apply(this))}
			</ul>
		</div>;
	}
}
