import React from 'react';
import SearchBar from './SearchBar';
import Results from './Results';
import {Grid} from '@material-ui/core';

export default class HomePage extends React.Component{
	constructor(props){
		super(props);
		this.state = {
			searchexp: '',
			searchres: [],
		}
	}

	handleSearchInput(e){
		this.setState({searchexp: e.target.value})
	}

	setSearchResults(results){
		console.log(results)
		this.setState({searchres: results})
	}

	getExp(){
		return this.state.searchexp;
	}

	getResults(){
		return this.state.searchres;
	}

	render(){
		return (
			<Grid container direction="column">
				<Grid item>
					<SearchBar exp={this.state.searchexp} handleInput={(e) => this.handleSearchInput(e)} setResults={(res) => this.setSearchResults(res)}/>
				</Grid>
				{this.state.searchres.length > 0
				? <Grid item>
					<Results results={this.state.searchres}/>
				</Grid>
				: <>
				</>
				}
			</Grid>
		)
	}
}
