import React from 'react';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
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
				<form onSubmit={e => this.getSearchResults(e)}>
					<TextField autoFocus onChange={(e) => this.handleInput(e)}/>
					<Button variant="contained" onClick={e => this.getSearchResults(e)}>Search</Button>
				</form>
		)
	}
}
