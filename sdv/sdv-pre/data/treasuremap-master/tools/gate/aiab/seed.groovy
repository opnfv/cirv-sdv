JOB_BASE = 'tools/gate/aiab'

pipelineJob("treasuremap-aiab") {

    logRotator{
        daysToKeep(90)
    }

    configure {
        node -> node / 'properties' / 'jenkins.branch.RateLimitBranchProperty_-JobPropertyImpl'{
            durationName 'hour'
            count '3'
        }
    }

    triggers {
        gerritTrigger {
            serverName('ATT-airship-CI')
            gerritProjects {
                gerritProject {
                    compareType('PLAIN')
                    pattern("airship/treasuremap")
                    branches {
                        branch {
                            compareType("ANT")
                            pattern("**")
                        }
                    }
                    disableStrictForbiddenFileVerification(false)
                }
            }
            triggerOnEvents {
                patchsetCreated {
                   excludeDrafts(false)
                   excludeTrivialRebase(false)
                   excludeNoCodeChange(false)
                }
                changeMerged()
                commentAddedContains {
                   commentAddedCommentContains('^recheck\$')
                }
            }
        }

        definition {
            cpsScm {
                scm {
                    git('https://review.opendev.org/airship/treasuremap')
                    scriptPath('tools/gate/aiab/Jenkinsfile')
                    lightweight(true)
                }
            }
        }
    }
}
