#!/usr/bin/perl
use Getopt::Std;
use File::KeePass;
my %options;
getopts('f:p:a:h', \%options);
$options{h} && usage();
sub usage
{
 print <<FILE;
lewm.pl  [-h] [-f FILENAME] [-p PASSFILENAME] [-a xsel_args]
FILE
exit;
}

sub copy2clip(){
  my ($key,$tip,$xsel_args,$value)= @_;
  print $key,'  :  ', " | $tip copied to clipboard \n";

    open FILE,  " | xsel -i ".$xsel_args
      or die $!;
    print FILE $value;
    close FILE;
        sleep 9;
        system("xsel -c ".$xsel_args);
}

my $file = $options{f} || 'kk.kdb';
my $xsel_args = $options{a} || ' ';
$master_pass = `$ENV{'LEPASS'}`;
chomp $master_pass;
$str1=$ARGV[0];
@egid=split /\./, $str1;
$gid =shift @egid;
$eid=join '.',@egid;
           my $k = File::KeePass->new;
           if (! eval { $k->load_db($file, $master_pass) }) {
               die "Couldn't load the file $file: $@";
           }

            my @all_groups_flattened = $k->find_groups({'title =~'=>$gid});
            my %ret=();
   foreach $group (@all_groups_flattened)
   {
     $gid=$group->{'id'};
           my @e = $k->find_entries({'title =~' => $eid ,group_id=>$gid});
           $k->unlock;
   foreach $column (@e)
  {
    $ret{$group->{'title'}.'.'.$column->{'title'}}=$column;
  }
}
$len3= keys %ret;
if ($len3 == 0)
{
  print "no record found \n";
}
elsif ($len3 == 1)
{
  while(($key, $value) = each(%ret))
 {
   &copy2clip ($key,"password" ,$xsel_args ,
     $value->{'password'});
   print "get username ? \n";
  chomp(my $key_1 = <STDIN>);
  if ($key_1 eq ''){
   &copy2clip ($key,"username" ,$xsel_args ,
     $value->{'username'});
  }
}
}
else
{
  while(($key, $value) = each(%ret))
 {
  print $key,'  :  ', $value->{'username'},"\n";
}
}
