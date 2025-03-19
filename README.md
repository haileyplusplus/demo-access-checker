# Access Checker

This is a simple utility to check access for an on-call employee. All example data is 
manually stored in the config/ subdirectory. 

## Running

The recommended way to run this utility is with docker compose, which will bring up both the 
frontend and backend. From the root directory:

```
% docker compose up --build
```

To run the utility outside of Docker, install the Python requirements for both the frontend and 
backend, change the hardcoded backend destination in the frontend 
(`BACKEND = 'http://backend:8099'`) to localhost or something else that's suitable, and bring up 
the frontends and backends.

## Notes

I've made the following assumptions in constructing these users, groups, resources, and access
profiles:

- Access profiles can represent a complete group of resources or permissions that are 
  needed to enable a certain workflow. These access profiles are considered to be roughly 
  equivalent to an environment. The system here demonstrates two separate imagined systems with 
  dev and prod environments for each. We also assume that only one access profile can be active 
  for a user at any given time as a defense against overprovisioned access.

- My choice of groups strikes a balance between project-specific roles and finer-grained 
  implementation details. For each of the two projects I have imagined different roles for that 
  project that an engineer might play. With the dev role they could have broad access to test 
  and make changes as needed in a development environment. With the release role they could 
  manage deployments to production and roll back releases. With the oncall role they would have 
  access to do emergency rollbacks as well as access to debugging tools in the prod environment. 
  VPN access for each project is its own separate role because I've imagined just one network 
  per project for simplicity. Corporate policies also allow tokens to be held for VPN access for 
  a longer length of time than for other resources.

- Group membership with time-bound access: Users join groups via some administrative interface 
  and are added to and removed from groups according to their job duties. This membership can be 
  time-bound on a scale of weeks or months (not modeled in this tool). For example, team members 
  of the Oxford project are normally added to Oxford groups depending on their role, but if a 
  member of the Oxford team needs to help out on the Green Light project they can also request 
  and add this membership.

- Access tokens: Membership in a group gives members the right to request temporary access 
  tokens. In the sample data, the amount of time a token is valid for a given group is given in 
  "token_hours" alongside each group. Token requests could be gated on any number of policies, 
  such as using a device that has the latest software updates, two-factor authentication, etc.

- Resources: These represent specific parts of the system that a user might need access to. 
  Access profiles are collections of resources, and permission to access resources is controlled 
  via group membership. A given resource may be available via more than one group.

- User interface: The user interface is designed to allow an on-call engineer to quickly see all 
  resources associated with a given profile and to check what might be needed to give them 
  access. The tool checks both group membership and time-bound token assignment. We imagine that 
  access can be requested through some sort of web interface, so the tool provides deep links to 
  mocks of profile switchers and token requestors. The tool also displays a warning when the 
  user has a token that will expire soon (the threshold for this is 1 hour) and provides a link 
  to optionally refresh the token.

- Scenarios: To simulate various users encountering this tool in a variety of different states, 
  I've created a few scenarios that highlight different states. Among them they should 
  comprehensively demonstrate all requested features. The /admin path on the frontend (not 
  linked from the tool) allows scenarios to be toggled as needed.
