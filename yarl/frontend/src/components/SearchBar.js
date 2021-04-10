import React from 'react';
import {InputBase, AppBar, Toolbar, IconButton, Grid, FormControl} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';
import MenuIcon from '@material-ui/icons/Menu';
import Results from './Results';
import SideBar from './SideBar'; 

export default class SearchBar extends React.Component{
	constructor(props){
		super(props);
		// this.setResults = props.setResults;
		// this.getExp = props.getExp;
		this.state = {
			toggled: false,
		}
	}

	handleInput(e){
		this.props.handleInput(e);
	}

	getSearchResults(e){
		e.preventDefault();
		fetch("/api/search" + "?exp=" + this.props.exp)
			.then(response => response.json())
			.then(results => this.props.setResults(results))
	}

	toggleMenu(val){
		if(val != null)
			this.setState({toggled: val});
		else
			this.setState({toggled: !this.state.toggled});
	}

	render() {
		const exp = this.props.exp;
		return (
			<>
				<AppBar position="sticky">
					<Toolbar component="form" onSubmit={e => this.getSearchResults(e)}>
						<IconButton edge='start' onClick={() => this.toggleMenu()}>
							{ this.state.toggled
								? <></>
								: <MenuIcon/>
							}
						</IconButton>
						<FormControl fullWidth>
							<InputBase 
								autoFocus 
								onChange={e => this.handleInput(e)} 
								placeholder="Search" 
							/>
						</FormControl>
						<IconButton onClick={e => this.getSearchResults(e)} >
							<SearchIcon/>
						</IconButton>
					</Toolbar>
				</AppBar>
				<SideBar toggled={this.state.toggled} setToggled={() => this.toggleMenu()}/>
			</>
		)
	}
}
