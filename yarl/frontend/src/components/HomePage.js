import React from 'react';
import SearchBar from './SearchBar';
import Results from './Results';

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
		this.setState({searchres: results})
	}

	getExp(){
		return this.state.searchexp;
	}

	getResults(){
		return this.state.searchres;
	}

	render(){return (
			<>
				<SearchBar getExp={() => this.getExp()} handleInput={(e) => this.handleSearchInput(e)} setResults={(res) => this.setSearchResults(res)}/>
				<Results getResults={() => this.getResults()}/>
			</>
		)
	}
}
