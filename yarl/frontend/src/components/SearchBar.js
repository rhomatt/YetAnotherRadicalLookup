import React from 'react';
import {InputBase, AppBar, Toolbar, IconButton, Grid, FormControl} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';
import Results from './Results';

export default class SearchBar extends React.Component{
	constructor(props){
		super(props);
		// this.setResults = props.setResults;
		// this.getExp = props.getExp;
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

	

	render() {
		const exp = this.props.exp;
		return (
			<AppBar position="static">
				<Toolbar component="form" onSubmit={e => this.getSearchResults(e)}>
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
		)
	}
}
