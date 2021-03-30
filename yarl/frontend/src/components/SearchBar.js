import React from 'react';
import {InputBase, AppBar, Toolbar, IconButton, Grid, FormControl} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';
import Results from './Results';

export default class SearchBar extends React.Component{
	constructor(props){
		super(props);
		this.handleInput = props.handleInput;
		this.setResults = props.setResults;
		this.getExp = props.getExp;
	}

	

	getSearchResults(e){
		e.preventDefault();
		fetch("/api/search" + "?exp=" + this.getExp())
			.then(response => response.json())
			.then(results => this.setResults(results))
	}

	render() {
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
