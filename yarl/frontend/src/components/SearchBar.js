import React from 'react';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Results from './Results';

export default class SearchBar extends React.Component{
	constructor(props){
		super(props);
		this.state = {
			searchexp: "",
			searchres: [],
		}
	}

	getSearchResults(e){
		e.preventDefault();
		fetch("/api/search" + "?exp=" + this.state.searchexp)
			.then(response => response.json())
			.then(results => this.setState({searchres: results}))
	}

	render() {
		return <Grid container spacing={2}>
					<Grid item xs={12} align="center">
						<form onSubmit={e => this.getSearchResults(e)}>
							<TextField onChange={(e) => this.setState({searchexp: e.target.value})}/>
							<Button variant="contained" onClick={e => this.getSearchResults(e)}>Search</Button>
						</form>
					</Grid>
					<Grid item xs={12} align="center">
						<Results results={this.state.searchres}/>
					</Grid>
				</Grid>;
	}
}
