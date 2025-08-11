from crewai import Agent,Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import load_dotenv
load_dotenv()

@CrewBase
class RsearchCrew():
    """ Research crew for comprehensive topic analysis and reporting"""

    agents: List[BaseAgent]
    tasks : List[Task]



    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher(self)->Agent:
        return Agent(
        config = self.agents_config['researcher'], 
        verbose = True,
        tools = [SerperDevTool()],
        allow_delegation=True
        )

    @agent
    def analyst(self)-> Agent:
        return Agent(
        config = self.agents_config['analyst'],
        verbose = True,
        allow_delegation=True
        )
    
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"]
        )
    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'], # type: ignore[index]
            output_file='output/report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  
            verbose=True,
        )


