#Fill in email and pass below
#Call like this perl script.pl (iso/package/laptop) testcase ...
#EG: perl script.pl iso 1200_testplanblah 1201_testplanblah

#!/usr/bin/perl
use strict;
use warnings;
use WWW::Mechanize;
use utf8;
use Encode;
use File::Path;
use File::Basename;
use Data::Dumper;

my $mech = WWW::Mechanize->new();

#login stuff
my $baseURL = '.qa.ubuntu.com';
#my $baseURL = '.qa.dev.stgraber.org';
my $adminURL = '/qatracker/admin';
my $testcaseURL = '/admin/config/services/qatracker/testcases/';
my $email = '';
my $password = '';

#web stuff
my $output;
my $testcaseTitle;
my $testcaseText;
my $testcasePage;
my $landingPage;

#testcase stuff
my $filename;
my $testcase;
my $testname;
my $testid;
my $newName;

#file stuff
my $path;

use open ':encoding(utf8)';

#my ($programName, $path) = fileparse($ARGV[0], '\[^\.]*');
#print "$programName - $path";
#die;

#first argument is the domain
my $domain = $ARGV[0];

#setup URL
$baseURL = 'http://'. $domain . $baseURL;

login();

#the rest is the files to push
foreach my $argnum (1 .. $#ARGV) {
    open(INPUT, "<$ARGV[$argnum]");
    open(INPUT, "<$ARGV[$argnum]") or die "Can't read file '$ARGV[$argnum]' [$!]\n";
    #read file contents into testcase string
    $testcase = do { local $/; <INPUT> };
    close (INPUT);
    #$testcase = encode('utf8',$testcase);

    #get the id and testcasename
    $filename = basename( $ARGV[$argnum] );
    #print "Processing arg $argnum argv $ARGV[$argnum] file $filename\n";
    #is this a new testcase?
    if ($filename =~ m!(.*)_(.*)!) {
        $testid = $1;
        $testname = $2;
    } else {
        $testid = "add";
        $testname = $filename;
    }

    #print "Looking at $testid - $testname\n";

    #open the testcase page
    loadTestcase();

    #fill in the form with values and submit
    $landingPage = updateTestcase();

    if ($testid eq "add") {
        #<a href="/admin/config/services/qatracker/testcases/1561/edit" class="module-link module-link-configure">
        #print "landingPage: $landingPage\n";
        $landingPage =~ m!<a href="/admin/config/services/qatracker/testcases/(.*)/edit" class="module-link module-link-configure">!;
        $testid = $1;
        ($filename, $path) = fileparse($ARGV[$argnum], '\[^\.]*');
        $newName = $path . $testid . '_' . $filename;
        print "Renaming test with $testid\n";
        rename $ARGV[$argnum], $newName;
    }
}

sub login {
    #http://iso.qa.ubuntu.com/qatracker/admin

    #login: <div><input type="hidden" value="https://login.ubuntu.com/" name="openid_identifier"></input><input id="edit-submit" class="form-submit" type="submit" value="Log in" name="op"></input><input type="hidden" value="http://iso.qa.ubuntu.com/openid/authenticate?destination=qatracker/admin" name="openid.return_to"></input><input type="hidden" value="form-R4STjLUV3JIExJq4A_4RuBZpy1wbKJ-U0qqmEXQg484" name="form_build_id"></input><input type="hidden" value="openid_launchpad_contents" name="form_id"></input>

    #    foreach ($mech->forms()) {
    #        print Dumper( $mech->current_form() );
    #    }

    #dev sites require you to authenticate to even see the site, then to do it again to login
    if (index($baseURL,"ps.qa.dev") != -1) {
        #load base page
        $mech->get($baseURL);
        if ($mech->success()) {
            #$output = $mech->content();
            #print "Base page:\n" . $output . "\n";
        } else {
            die localtime(time) . ' Error meching login' . "\n";
        }

        #submit login form
        $mech->submit_form(
            form_name => 'oid_form',
        );

        if ($mech->success()) {
            #$output = $mech->content();
            #print "Login submit:\n" . $output . "\n";
        } else {
            die localtime(time) . ' Error meching login' . "\n";
        }

        #submit redirect form
        #dev sites uses a different name
        $mech->submit_form(
            form_id => 'openid_message',
        );

        if ($mech->success()) {
            #$output = $mech->content();
            #print "Redirect submit:\n" . $output . "\n";
        } else {
            die localtime(time) . ' Error meching redirect' . "\n";
        }


        #submit sso login form
        $mech->submit_form(
            form_id => 'login-form',
            fields      => {
                email => $email,
                password => $password,
            }
        );

        if ($mech->success()) {
            #$output = $mech->content();
            #print "SSO Login submit:\n" . $output . "\n";
        } else {
            die localtime(time) . ' Error meching SSO Login' . "\n";
        }

        #sso decide form
        $mech->submit_form(
            form_name => 'decideform',
        );

        if ($mech->success()) {
            #$output = $mech->content();
            #print "SSO Decide submit:\n" . $output . "\n";
        } else {
            die localtime(time) . ' Error meching SSO Decide' . "\n";
        }

    }

    #load base page
    $mech->get($baseURL);
    if ($mech->success()) {
        #$output = $mech->content();
        #print "Base page:\n" . $output . "\n";
    } else {
        die localtime(time) . ' Error meching login' . "\n";
    }


    #submit login form
    $mech->submit_form(
        form_id => 'openid-launchpad-login-form',
    );

    if ($mech->success()) {
        #$output = $mech->content();
        #print "Login submit:\n" . $output . "\n";
    } else {
        die localtime(time) . ' Error meching login' . "\n";
    }

    #submit redirect form
    $mech->submit_form(
        form_id => 'openid-redirect-form',
    );

    if ($mech->success()) {
        #$output = $mech->content();
        #print "Redirect submit:\n" . $output . "\n";
    } else {
        die localtime(time) . ' Error meching redirect' . "\n";
    }

    #if coming from dev site login, skip straight to decide form
    if (index($baseURL,"ps.qa.dev") == -1) {
        #submit sso login form
        $mech->submit_form(
            form_id => 'login-form',
            fields      => {
                email => $email,
                password => $password,
            }
        );

        if ($mech->success()) {
            #$output = $mech->content();
            #print "SSO Login submit:\n" . $output . "\n";
        } else {
            die localtime(time) . ' Error meching SSO Login' . "\n";
        }
    }

    print "Enter your 2FA OTP: ";
    my $otp = <STDIN>;
    chomp $otp;

    $mech->submit_form(
        form_id => 'login-form',
        fields      => {
            oath_token => $otp,
        }
    );

    if ($mech->success()) {
        #$output = $mech->content();
        #print "2FA Login submit:\n" . $output . "\n";
    } else {
        die localtime(time) . ' Error meching 2FA Login' . "\n";
    }

    #sso decide form
    $mech->submit_form(
		form_name => 'decideform',
	);

    if ($mech->success()) {
        #$output = $mech->content();
        #print "SSO Decide submit:\n" . $output . "\n";
    } else {
        die localtime(time) . ' Error meching SSO Decide' . "\n";
    }

    #go to admin page
    $mech->get($baseURL . $adminURL);

    if ($mech->success()) {
        #$output = $mech->content();
        #print "Admin load:\n" . $output . "\n";
    } else {
        die localtime(time) . ' Error meching admin load' . "\n";
    }

    #save off testcase page for later parsing
    $mech->get($baseURL . $testcaseURL);
    if ($mech->success()) {
        $testcasePage = $mech->content();
        #print "testcase page:\n" . $testcasePage . "\n";
    } else {
        die localtime(time) . ' Error meching for testcasePage' . "\n";
    }
}

sub loadTestcase {
    #http://iso.qa.ubuntu.com/admin/config/services/qatracker/testcases/1471/edit
    #http://iso.qa.ubuntu.com/admin/config/services/qatracker/testcases/add

    if ($testid eq "add") {
        $mech->get($baseURL . $testcaseURL . "add");
    } else {
        $mech->get($baseURL . $testcaseURL . $testid . "/edit");
    }

    if ($mech->success()) {
        #$output = $mech->content();
        #print "Testcase load:\n" . $output . "\n";
    } else {
        die localtime(time) . ' Error meching Testcase load' . "\n";
    }

}

sub updateTestcase {

    #foreach ($mech->forms()) {
    #    print Dumper( $mech->current_form() );
    #}
    #print "\n\n\nTestid:$testid\n\n\nTestname:$testname\n\n\nTestcase:$testcase\n";
    #die;

    $mech->submit_form(
		form_id => 'qatracker-admin-testcases-edit',
        fields      => {
            #qatracker_testcase_id => $testid,
            qatracker_testcase_title => $testname,
            qatracker_testcase_revision_text => $testcase,
        }
	);

     if ($mech->success()) {
        $output = $mech->content();
        print "Testcase submitted $testid $testname\n";
        #print "Testcase submitted:\n" . $output . "\n";
        return $output;
    } else {
        die localtime(time) . ' Error submitting testcase update for ' . "$testid $testname\n";
    }
}
