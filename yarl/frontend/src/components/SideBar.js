import React from 'react';
import { Drawer, IconButton, List, ListItem, ListItemIcon, ListItemText, Divider } from '@material-ui/core';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
import GroupOutlinedIcon from '@material-ui/icons/GroupOutlined';
import MonetizationOnOutlinedIcon from '@material-ui/icons/MonetizationOnOutlined';
import {
    Link,
} from 'react-router-dom';

export default class SideBar extends React.Component {
	constructor(props){
		super(props);
	}

	toggleMenu(val){
		this.props.setToggled(val)
	}

	render(){
		let toggled = this.props.toggled;
		return (
            <Drawer
            varient="persistent"
            anchor="left"
            open={toggled}
            >
                <IconButton style={{marginLeft: "50%"}}edge="end" onClick={() => this.toggleMenu(false)}>
                    <ChevronLeftIcon/>
                </IconButton>
                <Divider/>
                <List>
                    { 
                        [
                            {
                                icon: <InfoOutlinedIcon/>, 
                                tag: "About",
                            }, 
                            {
                                icon: <GroupOutlinedIcon/>, 
                                tag: "Acknowledgements",
                            }, 
                            // {
                            //     icon: <MonetizationOnOutlinedIcon/>, 
                            //     tag: "Donate",
                            // }, 
                        ].map(item =>
                            <Link to={item.tag}>
                                <ListItem button key={item.tag}>
                                    <ListItemIcon>
                                        {item.icon}
                                    </ListItemIcon>
                                    <ListItemText primary={item.tag}/>
                                </ListItem>
                            </Link>
                        )
                    }
                </List>
            </Drawer>
		);
	}
}
