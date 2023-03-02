<?php
function translate($q, $sl, $tl){

    if($sl==$tl || $sl=='' || $tl==''){
        return $q;
    
    }
    else{
        $res="";

        $qqq=explode(".", $q);

        if(count($qqq)<2){

            @unlink($_SERVER['DOCUMENT_ROOT']."/transes.html");
            copy("http://translate.googleapis.com/translate_a/single?client=gtx&ie=UTF-8&oe=UTF-8&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&sl=".$sl."&tl=".$tl."&hl=hl&q=".urlencode($q), $_SERVER['DOCUMENT_ROOT']."/transes.html");
            if(file_exists($_SERVER['DOCUMENT_ROOT']."/transes.html")){
                $dara=file_get_contents($_SERVER['DOCUMENT_ROOT']."/transes.html");
                $f=explode("\"", $dara);

                $res.= $f[1];
            }
        }
        else{


        for($i=0;$i<(count($qqq)-1);$i++){

            if($qqq[$i]==' ' || $qqq[$i]==''){
            }
            else{
                copy("http://translate.googleapis.com/translate_a/single?client=gtx&ie=UTF-8&oe=UTF-8&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&sl=".$sl."&tl=".$tl."&hl=hl&q=".urlencode($qqq[$i]), $_SERVER['DOCUMENT_ROOT']."/transes.html");

                $dara=file_get_contents($_SERVER['DOCUMENT_ROOT']."/transes.html");
                @unlink($_SERVER['DOCUMENT_ROOT']."/transes.html");
                $f=explode("\"", $dara);

                $res.= $f[1].". ";
                }
            }
        }
        return $res;
    }

}




echo(translate("Goede dag dames en heren", "nl", "en"));
?>