#export env setting
if [ -z $1 ] ; then
    #homedir=/tmp/hpda/next/semeval
    homedir=$HOME/hpda/semeval
else
    homedir=$1
fi
export _semevalproject_=$homedir
export PYTHONPATH=$_semevalproject_/src/:$PYTHONPATH

#set up alias
#alias baggingTest="python -m programTester.baggingTest.test_content"
#alias items2html="python -m programTester.baggingTest.items2html"


