import React from 'react';
import { Drawer, IconButton, Divider } from '@material-ui/core';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';

export default class SideBar extends React.Component {
	constructor(props){
		super(props);
	}

	toggleMenu(){
		this.props.setToggled()
	}

	render(){
		let toggled = this.props.toggled;
		return (
			<Drawer
			varient="persistent"
			anchor="left"
			open={toggled}
			>
				<IconButton onClick={() => this.toggleMenu()}>
					<ChevronRightIcon/>
				</IconButton>
			</Drawer>
		);
	}
}
