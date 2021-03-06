import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    this.setState({page: num}, () => {
      if (this.state.currentCategory) {
        this.getByCategory(this.state.currentCategory, this.state.page)
      } else {
        this.getQuestions()
      }
    });
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getByCategory= (id, page=1) => {
    $.ajax({
      url: `/questions?category=${id}&page=${page}`,
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/search`,
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({search_term: searchTerm}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`,
          type: "DELETE",
          success: (result) => {
            this.setState(prevState => {
              // check if the removed item was the last item on the page
              const page = this.state.totalQuestions - ((this.state.page - 1) * 10) === 1
                ? prevState.page - 1
                : prevState.page
              return {
                totalQuestions: prevState.totalQuestions - 1,
                page
              }
            }, () => {
              if (this.state.currentCategory) {
                this.getByCategory(this.state.currentCategory, this.state.page)
              } else {
                this.getQuestions()
              }
            })
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }

  render() {
    const headingStyle = this.state.currentCategory
      ? {fontWeight: 'normal'}
      : {fontWeight: 'bold'}

    return (
      <div className="question-view">
        <div className="categories-list">
          <h2 style={headingStyle} onClick={() => {this.getQuestions()}}>Categories</h2>
          <ul>
            {Object.keys(this.state.categories).map((id, ) => { 
              const style = this.state.currentCategory === parseInt(id)
                ? {fontWeight: 'bold'}
                : null
              return (
                <li key={id} style={style} onClick={() => {this.getByCategory(id)}}>
                  {this.state.categories[id]}
                  <img className="category" src={`${this.state.categories[id]}.svg`}/>
                </li>
              )
            })}
          </ul>
          <Search submitSearch={this.submitSearch}/>
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={this.state.categories[q.category]} 
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className="pagination-menu">
            {this.createPagination()}
          </div>
        </div>

      </div>
    );
  }
}

export default QuestionView;
